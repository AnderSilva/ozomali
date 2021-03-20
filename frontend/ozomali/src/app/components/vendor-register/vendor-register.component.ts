import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { Subject } from 'rxjs';
import {
  debounceTime,
  filter,
  switchMap,
  take,
  takeUntil,
} from 'rxjs/operators';
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

  constructor(
    private formBuider: FormBuilder,
    private addressService: AddressService,
    private vendorService: VendorService,
    private dialog: MatDialog
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
  }

  ngOnInit(): void {
    this.vendorRegisterForm
      .get('cep')
      .valueChanges.pipe(
        takeUntil(this.unsubscribe$),
        filter((cep) => cep && cep.length === 8),
        debounceTime(300),
        switchMap((cep) => {
          this.isAddressLoading = true;
          return this.addressService.getAddress(cep);
        })
      )
      .subscribe((address) => {
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
  }

  public registerVendor(): void {
    if (this.vendorRegisterForm.invalid || this.isRegisterLoading) {
      return;
    }

    const modal = this.dialog.open(ConfirmationModalComponent);
    modal.componentInstance.description =
      'Você realmente quer salvar esse cadastro?';
    modal.componentInstance.confirmText = 'Sim';
    modal.componentInstance.cancelText = 'Não';

    modal.componentInstance.confirmation
      .pipe(
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
        take(1)
      )
      .subscribe(
        () => {
          this.vendorRegisterForm.reset();
          this.isRegisterLoading = false;
          const modal = this.dialog.open(FeedbackModalComponent);
          modal.componentInstance.text = 'Cadastro Realizado com Sucesso!';
          modal.componentInstance.continueText = 'Fechar';
        },
        () => {
          this.isRegisterLoading = false;
          const modal = this.dialog.open(FeedbackModalComponent);
          modal.componentInstance.text = 'Desculpe, o cadastro não funcionou!';
          modal.componentInstance.warning =
            'Tente novamente ou entre em contado com nosso suporte.';
          modal.componentInstance.continueText = 'Fechar';
        }
      );
  }
}
