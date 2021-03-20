import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Subject } from 'rxjs';
import { debounceTime, filter, switchMap, takeUntil } from 'rxjs/operators';
import { AddressService } from 'src/app/services/address.service';

@Component({
  selector: 'app-vendor-register',
  templateUrl: './vendor-register.component.html',
  styleUrls: ['./vendor-register.component.scss'],
})
export class VendorRegisterComponent implements OnInit, OnDestroy {
  private readonly unsubscribe$: Subject<void> = new Subject<void>();
  public isLoading: boolean = false;
  public vendorRegisterForm: FormGroup;

  constructor(
    private formBuider: FormBuilder,
    private addressService: AddressService
  ) {
    this.vendorRegisterForm = this.formBuider.group({
      cnpj: ['', Validators.required],
      nome: ['', Validators.required],
      cep: ['', Validators.required],
      endereco: ['', Validators.required],
      numero: ['', Validators.required],
      complemento: [''],
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
          this.isLoading = true;
          return this.addressService.getAddress(cep);
        })
      )
      .subscribe((address) => {
        this.isLoading = false;
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
}
