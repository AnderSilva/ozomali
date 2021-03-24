import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { Subject } from 'rxjs';
import { debounceTime, filter, switchMap, take, takeUntil } from 'rxjs/operators';
import { vendor } from 'src/app/interfaces/vendor.interface';
import { AddressService } from 'src/app/services/address.service';
import { VendorService } from 'src/app/services/vendor.service';
import { ConfirmationModalComponent } from '../confirmation-modal/confirmation-modal.component';
import { FeedbackModalComponent } from '../feedback-modal/feedback-modal.component';

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
  public vendor: vendor;
  @Input() public isSearch: boolean;

  constructor(
    private formBuider: FormBuilder,
    private addressService: AddressService,
    private vendorService: VendorService,
    private dialog: MatDialog,
  ) {
    this.vendorRegisterForm = this.formBuider.group({
      cnpj: ['', Validators.required],
      nome: ['', Validators.required],
      cep: ['', Validators.required],
      endereco: ['', Validators.required],
      numero: ['', Validators.required],
      complemento: ['', Validators.required],
      cidade: ['', Validators.required],
      estado: ['', Validators.required],
    });

    this.vendorSearchForm = this.formBuider.group({
      id: ['', Validators.required],
    });
  }

  ngOnInit(): void {
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

  ngOnDestroy(): void {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  public setAddress(address: any): void {
    this.vendorRegisterForm.get('endereco').setValue(address.logradouro);
    this.vendorRegisterForm.get('cidade').setValue(address.localidade);
    this.vendorRegisterForm.get('estado').setValue(address.uf);
  }

  public clearForm(): void {
    this.vendorRegisterForm.reset();
    this.vendor = undefined;
  }

  public registerVendor(): void {
    if (this.vendorRegisterForm.invalid || this.isRegisterLoading) {
      this.vendorRegisterForm.markAllAsTouched();
      return;
    }

    const confirmationModal = this.dialog.open(ConfirmationModalComponent, {
      data: {
        description: 'Você realmente quer salvar esse cadastro?',
        confirmText: 'Sim',
        cancelText: 'Não',
      },
    });

    confirmationModal
      .afterClosed()
      .pipe(
        filter(confirmation => confirmation === true),
        switchMap(() => {
          this.isRegisterLoading = true;
          const formValues = this.vendorRegisterForm.getRawValue();
          let params: vendor = {};

          Object.entries(formValues).forEach(([key, value]) => {
            if (value) {
              params[`${key}`] = value;
            }
          });

          return this.vendorService.createVendor(params);
        }),
        take(1),
      )
      .subscribe(
        () => {
          this.vendorRegisterForm.reset();
          this.isRegisterLoading = false;
          const feedbackModal = this.dialog.open(FeedbackModalComponent, {
            data: {
              text: 'Cadastro Realizado com Sucesso!',
              continueText: 'Fechar',
            },
          });
        },
        () => {
          this.isRegisterLoading = false;
          const feedbackModal = this.dialog.open(FeedbackModalComponent, {
            data: {
              text: 'Desculpe, o cadastro não funcionou!',
              warning: 'Tente novamente ou entre em contado com nosso suporte.',
              continueText: 'Fechar',
            },
          });
        },
      );
  }

  public onSearchVendor(): void {
    if (this.vendorSearchForm.invalid || this.isRegisterLoading) {
      this.vendorSearchForm.markAllAsTouched();
      return;
    }

    this.isRegisterLoading = true;
    const id = this.vendorSearchForm.get('id').value;

    this.vendorService
      .getVendorById(id)
      .pipe(take(1))
      .subscribe(
        vendor => {
          this.isRegisterLoading = false;
          this.vendor = vendor[0];
          this.setVendorForm(this.vendor);
        },
        () => {
          this.isRegisterLoading = false;
          const feedbackModal = this.dialog.open(FeedbackModalComponent, {
            data: {
              text: 'Desculpe, ocorreu um erro!',
              warning: 'Tente novamente ou entre em contado com nosso suporte.',
              continueText: 'Fechar',
            },
          });
        },
      );
  }

  public setVendorForm(vendor: vendor): void {
    this.vendorRegisterForm.get('cnpj').setValue(vendor.cnpj);
    this.vendorRegisterForm.get('nome').setValue(vendor.nome);
    this.vendorRegisterForm.get('cep').setValue(vendor.cep);
    this.vendorRegisterForm.get('endereco').setValue(vendor.endereco);
    this.vendorRegisterForm.get('numero').setValue(vendor.numero);
    this.vendorRegisterForm.get('complemento').setValue(vendor.complemento);
    this.vendorRegisterForm.get('cidade').setValue(vendor.cidade);
    this.vendorRegisterForm.get('estado').setValue(vendor.estado);
  }

  public deleteVendor(): void {
    if (this.isRegisterLoading) {
      return;
    }

    const confirmationModal = this.dialog.open(ConfirmationModalComponent, {
      data: {
        description: 'Você realmente quer apagar esse registro?',
        warning: 'Uma vez apagado, não será possivel recuperar',
        confirmText: 'Sim',
        cancelText: 'Não',
      },
    });

    confirmationModal
      .afterClosed()
      .pipe(
        filter(confirmation => confirmation === true),
        switchMap(() => {
          this.isRegisterLoading = true;

          return this.vendorService.deleteVendorById(this.vendor.id);
        }),
        take(1),
      )
      .subscribe(
        () => {
          this.vendorRegisterForm.reset();
          this.isRegisterLoading = false;
          this.vendor = undefined;
          const feedbackModal = this.dialog.open(FeedbackModalComponent, {
            data: {
              text: 'Registro apagado com sucesso!',
              continueText: 'Fechar',
            },
          });
        },
        () => {
          this.isRegisterLoading = false;
          const feedbackModal = this.dialog.open(FeedbackModalComponent, {
            data: {
              text: 'Desculpe, ocorreu um erro!',
              warning: 'Tente novamente ou entre em contado com nosso suporte.',
              continueText: 'Fechar',
            },
          });
        },
      );
  }

  public updateVendor(): void {
    if (this.vendorRegisterForm.invalid || this.isRegisterLoading) {
      this.vendorRegisterForm.markAllAsTouched();
      return;
    }

    this.isRegisterLoading = true;
    const formValues = this.vendorRegisterForm.getRawValue();
    let params: vendor = {};

    Object.entries(formValues).forEach(([key, value]) => {
      if (value) {
        params[`${key}`] = value;
      }
    });

    params = { ...params, id: this.vendor.id };
    params.cep = params.cep.toString();

    this.vendorService
      .updateVendor(params)
      .pipe(take(1))
      .subscribe(
        () => {
          this.isRegisterLoading = false;
          const feedbackModal = this.dialog.open(FeedbackModalComponent, {
            data: {
              text: 'Registro atualizado com sucesso!',
              continueText: 'Fechar',
            },
          });
        },
        () => {
          this.isRegisterLoading = false;
          const feedbackModal = this.dialog.open(FeedbackModalComponent, {
            data: {
              text: 'Desculpe, ocorreu um erro!',
              warning: 'Tente novamente ou entre em contado com nosso suporte.',
              continueText: 'Fechar',
            },
          });
        },
      );
  }
}
