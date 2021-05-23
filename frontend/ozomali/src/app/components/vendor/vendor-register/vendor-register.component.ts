import { Component, EventEmitter, Input, OnDestroy, OnInit, Output, SimpleChanges } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Subject } from 'rxjs';
import { debounceTime, filter, switchMap, take, takeUntil } from 'rxjs/operators';
import { AddressService } from 'src/app/services/address/address.service';
import { NotificationService } from 'src/app/services/notification/notification.service';
import { VendorService } from 'src/app/services/vendor/vendor.service';

@Component({
  selector: 'app-vendor-register',
  templateUrl: './vendor-register.component.html',
  styleUrls: ['./vendor-register.component.scss'],
})
export class VendorRegisterComponent implements OnInit, OnDestroy {
  private readonly unsubscribe$: Subject<void> = new Subject<void>();
  public isAddressLoading: boolean = false;
  public isRegisterLoading: boolean = false;
  public vendorRegisterForm: FormGroup;
  public vendorSearchForm: FormGroup;
  public mask: string;

  @Input() public vendor: any;
  @Input() public isSearch: boolean;
  @Output() public results = new EventEmitter<any>();
  @Output() public clearSearch = new EventEmitter<any>();

  constructor(
    private formBuider: FormBuilder,
    private addressService: AddressService,
    private vendorService: VendorService,
    private notifications: NotificationService,
  ) {
    this.vendorRegisterForm = this.formBuider.group({
      cnpj: ['', Validators.required],
      nome: ['', Validators.required],
      cep: ['', Validators.required],
      logradouro: ['', Validators.required],
      numero: ['', Validators.required],
      complemento: [''],
      bairro: ['', Validators.required],
      cidade: ['', Validators.required],
      estado: ['', Validators.required],

      ativo: [''],
      id: [{ value: '', disabled: true }],
    });

    this.vendorSearchForm = this.formBuider.group({
      filter: ['', Validators.required],
      status: [''],
      param: [''],
    });
  }

  ngOnInit(): void {
    if (this.isSearch) {
      this.vendorRegisterForm.controls['cnpj'].disable();
    }

    this.vendorRegisterForm
      .get('cep')
      .valueChanges.pipe(
        takeUntil(this.unsubscribe$),
        filter(cep => cep && cep.length === 8),
        debounceTime(300),
        switchMap(cep => {
          this.isAddressLoading = true;
          return this.addressService.getAddress(cep);
        }),
      )
      .subscribe(address => {
        this.isAddressLoading = false;
        this.setAddress(address);
      });
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes.vendor.currentValue !== changes.vendor.previousValue) {
      this.setVendorForm(this.vendor);
    }
  }

  ngOnDestroy(): void {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  public setAddress(address: any): void {
    this.vendorRegisterForm.get('logradouro').setValue(address.logradouro);
    this.vendorRegisterForm.get('bairro').setValue(address.bairro);
    this.vendorRegisterForm.get('cidade').setValue(address.localidade);
    this.vendorRegisterForm.get('estado').setValue(address.uf);
  }

  public clearForm(): void {
    this.clearSearch.emit();
    this.vendorRegisterForm.reset();
    this.vendor = undefined;
  }

  public updateMask(filter: string): void {
    this.vendorSearchForm.get('param').reset();

    switch (filter) {
      case 'id':
      case 'numero':
        this.mask = '999999999999999999999999';
        break;
      case 'cnpj':
        this.mask = 'CPF_CNPJ';
        break;
      case 'cep':
        this.mask = '00000-000';
        break;
      case 'estado':
        this.mask = 'SS';
        break;
      default:
        this.mask = '';
        break;
    }
  }

  public registerVendor(): void {
    if (this.vendorRegisterForm.invalid || this.isRegisterLoading) {
      this.vendorRegisterForm.markAllAsTouched();
      return;
    }

    const confirmationModal = this.notifications.confirmationModal(
      'Você realmente quer salvar esse cadastro?',
      'Sim',
      'Não',
    );

    confirmationModal
      .afterClosed()
      .pipe(
        filter(confirmation => confirmation === true),
        switchMap(() => {
          this.isRegisterLoading = true;
          const formValues = this.vendorRegisterForm.getRawValue();

          return this.vendorService.createVendor(formValues);
        }),
        take(1),
      )
      .subscribe(
        response => {
          this.vendorRegisterForm.reset();
          this.isRegisterLoading = false;
          this.notifications.feedbackModal(response);
        },
        response => {
          this.isRegisterLoading = false;
          this.notifications.feedbackModal(response);
        },
      );
  }

  public onSearchVendor(): void {
    if (this.vendorSearchForm.invalid || this.isRegisterLoading) {
      this.vendorSearchForm.markAllAsTouched();
      return;
    }

    this.isRegisterLoading = true;
    let search: any = {};
    search[this.vendorSearchForm.get('filter').value] = this.vendorSearchForm.get('param').value;

    if ('id' in search) {
      search.id = Number(search.id);
    }
    if ('ativo' in search) {
      search.ativo = this.vendorSearchForm.get('status').value;
    }

    this.vendorService
      .searchVendor(search)
      .pipe(take(1))
      .subscribe(
        vendors => {
          this.isRegisterLoading = false;
          this.results.emit(vendors.data);
        },
        response => {
          this.isRegisterLoading = false;
          this.notifications.feedbackModal(response);
        },
      );
  }

  public setVendorForm(vendor: any): void {
    this.vendorRegisterForm.get('cnpj').setValue(vendor.cnpj);
    this.vendorRegisterForm.get('nome').setValue(vendor.nome);
    this.vendorRegisterForm.get('cep').setValue(vendor.cep);
    this.vendorRegisterForm.get('logradouro').setValue(vendor.logradouro);
    this.vendorRegisterForm.get('numero').setValue(vendor.numero);
    this.vendorRegisterForm.get('complemento').setValue(vendor.complemento);
    this.vendorRegisterForm.get('bairro').setValue(vendor.bairro);
    this.vendorRegisterForm.get('cidade').setValue(vendor.cidade);
    this.vendorRegisterForm.get('estado').setValue(vendor.estado);

    this.vendorRegisterForm.get('id').setValue(vendor.id);
    this.vendorRegisterForm.get('ativo').setValue(vendor.ativo);
  }

  public getVendors(): void {
    if (this.isRegisterLoading) {
      return;
    }

    this.isRegisterLoading = true;

    this.vendorService
      .getVendors()
      .pipe(take(1))
      .subscribe(
        vendors => {
          this.isRegisterLoading = false;
          this.results.emit(vendors.data);
        },
        response => {
          this.isRegisterLoading = false;
          this.notifications.feedbackModal(response);
        },
      );
  }

  public updateVendor(): void {
    if (this.vendorRegisterForm.invalid || this.isRegisterLoading) {
      this.vendorRegisterForm.markAllAsTouched();
      return;
    }

    this.isRegisterLoading = true;
    let formValues = this.vendorRegisterForm.getRawValue();

    this.vendorService
      .updateVendor(this.vendor.id, formValues)
      .pipe(take(1))
      .subscribe(
        response => {
          this.isRegisterLoading = false;
          this.notifications.feedbackModal(response);
        },
        response => {
          this.isRegisterLoading = false;
          this.notifications.feedbackModal(response);
        },
      );
  }
}
