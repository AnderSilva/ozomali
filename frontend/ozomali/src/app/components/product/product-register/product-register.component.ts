import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Observable } from 'rxjs';
import { filter, map, startWith, switchMap, take } from 'rxjs/operators';
import { NotificationService } from 'src/app/services/notification/notification.service';
import { ProductService } from 'src/app/services/product/product.service';

@Component({
  selector: 'app-product-register',
  templateUrl: './product-register.component.html',
  styleUrls: ['./product-register.component.scss'],
})
export class ProductRegisterComponent implements OnChanges, OnInit {
  @Input() public isSearch: boolean;
  @Output() public results = new EventEmitter<any>();
  @Output() public clearSearch = new EventEmitter<any>();
  @Input() public product: any;

  @Input() public vendors: any;
  @Input() public vendorNames: string[];

  public filteredVendors: Observable<string[]>;
  public fornecedor: FormControl;

  public productRegisterForm: FormGroup;
  public productSearchForm: FormGroup;
  public isRegisterLoading: boolean;
  public mask: string;

  constructor(
    private formBuilder: FormBuilder,
    private productService: ProductService,
    private notifications: NotificationService,
  ) {
    this.fornecedor = new FormControl('', Validators.required);

    this.productRegisterForm = this.formBuilder.group({
      nome: ['', Validators.required],
      codigo_barra: ['', Validators.required],
      fornecedor_id: ['', Validators.required],
      preco_venda: ['', Validators.required],

      ativo: [''],
      id: [{ value: '', disabled: true }],
      saldo: [{ value: '', disabled: true }],
    });

    this.productSearchForm = this.formBuilder.group({
      filter: ['', Validators.required],
      status: [''],
      price: [''],
      param: ['', Validators.required],
    });
  }

  ngOnInit(): void {
    this.filteredVendors = this.fornecedor.valueChanges.pipe(
      startWith(''),
      map(value => this.filterVendors(value)),
    );
  }

  private filterVendors(value: string): string[] {
    const filterValue = value?.toLowerCase();

    return this.vendorNames.filter(option => option?.toLowerCase().includes(filterValue));
  }

  public vendorChosen(vendorName: string): void {
    const matchVendor = this.vendors.find((vendor: any) => vendor.nome === vendorName);

    this.productRegisterForm.get('fornecedor_id').setValue(matchVendor.id);
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.product?.currentValue !== changes.product?.previousValue) {
      this.setProductForm(this.product);
    }
  }

  public clearForm(): void {
    this.clearSearch.emit();
    this.productRegisterForm.reset();
    this.fornecedor.reset();
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

  public updateMask(filterValue: string): void {
    this.productSearchForm.get('param').reset();

    switch (filterValue) {
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
    if (this.productRegisterForm.invalid || this.fornecedor.invalid || this.isRegisterLoading) {
      this.productRegisterForm.markAllAsTouched();
      this.fornecedor.markAsTouched();
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

          delete formValues.id;
          delete formValues.ativo;
          delete formValues.saldo;

          formValues.fornecedor_id = Number(formValues.fornecedor_id);

          return this.productService.createProduct(formValues);
        }),
        take(1),
      )
      .subscribe(
        response => {
          this.productRegisterForm.reset();
          this.fornecedor.reset();
          this.isRegisterLoading = false;
          this.notifications.feedbackModal(response);
        },
        response => {
          this.isRegisterLoading = false;
          this.notifications.feedbackModal(response);
        },
      );
  }

  public setProductForm(productReceived: any): void {
    this.productRegisterForm.get('nome').setValue(productReceived.nome);
    this.productRegisterForm.get('codigo_barra').setValue(productReceived.codigo_barra);
    this.productRegisterForm.get('fornecedor_id').setValue(productReceived.fornecedor_id);
    this.productRegisterForm.get('preco_venda').setValue(productReceived.preco_venda);

    this.productRegisterForm.get('ativo').setValue(productReceived.ativo);
    this.productRegisterForm.get('id').setValue(productReceived.id);
    this.productRegisterForm.get('saldo').setValue(productReceived.saldo);

    this.fornecedor.setValue(productReceived.nome_fornecedor);
  }

  public onSearchProduct(): void {
    if (this.productSearchForm.invalid || this.isRegisterLoading) {
      this.productSearchForm.markAllAsTouched();
      return;
    }

    this.isRegisterLoading = true;

    const search: any = {};
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
        resultProduct => {
          this.isRegisterLoading = false;
          this.results.emit(resultProduct.data);
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
    if (this.productRegisterForm.invalid || this.fornecedor.invalid || this.isRegisterLoading) {
      this.productRegisterForm.markAllAsTouched();
      this.fornecedor.markAsTouched();
      return;
    }

    this.isRegisterLoading = true;
    const formValues = this.productRegisterForm.getRawValue();

    delete formValues.id;
    delete formValues.saldo;

    formValues.fornecedor_id = Number(formValues.fornecedor_id);

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
