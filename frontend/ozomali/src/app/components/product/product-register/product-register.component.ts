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

  constructor(
    private formBuider: FormBuilder,
    private productService: ProductService,
    private notifications: NotificationService,
  ) {
    this.productRegisterForm = this.formBuider.group({
      nome: ['', Validators.required],
      codigo_barra: ['', Validators.required],
      fornecedor_id: ['', Validators.required],
      preco: ['', Validators.required],

      ativo: [''],
      id: [{ value: '', disabled: true }],
    });

    this.productSearchForm = this.formBuider.group({
      id: ['', Validators.required],
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
    this.productRegisterForm.get('preco').setValue(product.preco);

    this.productRegisterForm.get('id').setValue(product.id);
    this.productRegisterForm.get('ativo').setValue(product.ativo);
  }

  public onSearchProduct(): void {
    if (this.productSearchForm.invalid || this.isRegisterLoading) {
      this.productSearchForm.markAllAsTouched();
      return;
    }

    this.isRegisterLoading = true;
    const id = this.productSearchForm.get('id').value;

    this.productService
      .getProductById(id)
      .pipe(take(1))
      .subscribe(
        product => {
          this.isRegisterLoading = false;
          this.results.emit(product);
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
