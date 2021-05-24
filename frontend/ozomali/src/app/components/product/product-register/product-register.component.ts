import { Component, EventEmitter, Input, OnInit, Output, SimpleChanges } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { filter, switchMap, take } from 'rxjs/operators';
import { product } from 'src/app/interfaces/product.interface';
import { NotificationService } from 'src/app/services/notification/notification.service';
import { ProductService } from 'src/app/services/product/product.service';

@Component({
  selector: 'app-product-register',
  templateUrl: './product-register.component.html',
  styleUrls: ['./product-register.component.scss'],
})
export class ProductRegisterComponent implements OnInit {
  @Input() public isSearch: boolean;
  @Output() public results = new EventEmitter<any>();
  @Output() public clearSearch = new EventEmitter<any>();
  @Input() public product: product;

  public productRegisterForm: FormGroup;
  public productSearchForm: FormGroup;
  public isRegisterLoading: boolean;
  public mask: string;

  constructor(
    private formBuilder: FormBuilder,
    private productService: ProductService,
    private notifications: NotificationService,
  ) {
    this.productRegisterForm = this.formBuilder.group({
      nome: ['', Validators.required],
      codigo_barra: ['', Validators.required],
      fornecedor_id: ['', Validators.required],
      preco_venda: ['', Validators.required],

      ativo: [''],
      id: [{ value: '', disabled: true }],
      nome_fornecedor: [{ value: '', disabled: true }],
      saldo: [{ value: '', disabled: true }],
    });

    this.productSearchForm = this.formBuilder.group({
      filter: ['', Validators.required],
      status: [''],
      price: [''],
      param: ['', Validators.required],
    });
  }

  ngOnInit(): void {}

  ngOnChanges(changes: SimpleChanges) {
    if (changes.product.currentValue !== changes.product.previousValue) {
      this.setProductForm(this.product);
    }
  }

  public clearForm(): void {
    this.clearSearch.emit();
    this.productRegisterForm.reset();
    this.product = undefined;
  }

  public updateValidity(value: string): void {
    const paramInput = this.productSearchForm.get('param');
    const priceInput = this.productSearchForm.get('price');
    const statusInput = this.productSearchForm.get('status');

    switch (value) {
      case 'ativo':
        paramInput.setValidators(null);
        priceInput.setValidators(null);
        statusInput.setValidators(Validators.required);
        break;
      case 'preco_venda_ini':
      case 'preco_venda_fin':
        paramInput.setValidators(null);
        statusInput.setValidators(null);
        priceInput.setValidators(Validators.required);
        break;
      default:
        priceInput.setValidators(null);
        statusInput.setValidators(null);
        paramInput.setValidators(Validators.required);
        break;
    }

    paramInput.updateValueAndValidity();
    priceInput.updateValueAndValidity();
    statusInput.updateValueAndValidity();
  }

  public updateMask(filter: string): void {
    this.productSearchForm.get('param').reset();

    switch (filter) {
      case 'id':
      case 'codigo_barra':
        this.mask = '999999999999999999999999';
        break;
      default:
        this.mask = '';
        break;
    }
  }

  public registerProduct(): void {
    if (this.productRegisterForm.invalid || this.isRegisterLoading) {
      this.productRegisterForm.markAllAsTouched();
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
          const formValues = this.productRegisterForm.getRawValue();

          formValues.fornecedor_id = Number(formValues.fornecedor_id);

          return this.productService.createProduct(formValues);
        }),
        take(1),
      )
      .subscribe(
        response => {
          this.productRegisterForm.reset();
          this.isRegisterLoading = false;
          this.notifications.feedbackModal(response);
        },
        response => {
          this.isRegisterLoading = false;
          this.notifications.feedbackModal(response);
        },
      );
  }

  public setProductForm(product: any): void {
    this.productRegisterForm.get('nome').setValue(product.nome);
    this.productRegisterForm.get('codigo_barra').setValue(product.codigo_barra);
    this.productRegisterForm.get('fornecedor_id').setValue(product.fornecedor_id);
    this.productRegisterForm.get('preco_venda').setValue(product.preco_venda);

    this.productRegisterForm.get('ativo').setValue(product.ativo);
    this.productRegisterForm.get('id').setValue(product.id);
    this.productRegisterForm.get('nome_fornecedor').setValue(product.nome_fornecedor);
    this.productRegisterForm.get('saldo').setValue(product.saldo);
  }

  public onSearchProduct(): void {
    if (this.productSearchForm.invalid || this.isRegisterLoading) {
      this.productSearchForm.markAllAsTouched();
      return;
    }

    this.isRegisterLoading = true;

    let search: any = {};
    search[this.productSearchForm.get('filter').value] = this.productSearchForm.get('param').value;

    if ('id' in search) {
      search.id = Number(search.id);
    }
    if ('ativo' in search) {
      search.ativo = this.productSearchForm.get('status').value;
    }
    if ('preco_venda_ini' in search) {
      search.preco_venda_ini = this.productSearchForm.get('price').value;
    }
    if ('preco_venda_fin' in search) {
      search.preco_venda_fin = this.productSearchForm.get('price').value;
    }

    this.productService
      .searchProduct(search)
      .pipe(take(1))
      .subscribe(
        product => {
          this.isRegisterLoading = false;
          this.results.emit(product.data);
        },
        response => {
          this.isRegisterLoading = false;
          this.notifications.feedbackModal(response);
        },
      );
  }

  public getProducts(): void {
    if (this.isRegisterLoading) {
      return;
    }

    this.isRegisterLoading = true;

    this.productService
      .getProducts()
      .pipe(take(1))
      .subscribe(
        products => {
          this.isRegisterLoading = false;
          this.results.emit(products.data);
        },
        response => {
          this.isRegisterLoading = false;
          this.notifications.feedbackModal(response);
        },
      );
  }

  public updateProduct(): void {
    if (this.productRegisterForm.invalid || this.isRegisterLoading) {
      this.productRegisterForm.markAllAsTouched();
      return;
    }

    this.isRegisterLoading = true;
    let formValues = this.productRegisterForm.getRawValue();

    this.productService
      .updateProduct(this.product.id, formValues)
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
