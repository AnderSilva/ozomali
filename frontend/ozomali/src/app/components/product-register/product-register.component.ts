import { Component, Input, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { filter, switchMap, take } from 'rxjs/operators';
import { product } from 'src/app/interfaces/product.interface';
import { ProductService } from 'src/app/services/product.service';
import { ConfirmationModalComponent } from '../confirmation-modal/confirmation-modal.component';
import { FeedbackModalComponent } from '../feedback-modal/feedback-modal.component';

@Component({
  selector: 'app-product-register',
  templateUrl: './product-register.component.html',
  styleUrls: ['./product-register.component.scss'],
})
export class ProductRegisterComponent implements OnInit {
  @Input() public isSearch: boolean;
  public product: product;
  public productRegisterForm: FormGroup;
  public productSearchForm: FormGroup;
  public isRegisterLoading: boolean;
  public number: number

  constructor(private formBuider: FormBuilder, private productService: ProductService, private dialog: MatDialog) {
    this.productRegisterForm = this.formBuider.group({
      nome: ['', Validators.required],
      preco_custo: ['', Validators.required],
      preco_venda: ['', Validators.required],
      quantidade: ['', Validators.required],
    });

    this.productSearchForm = this.formBuider.group({
      id: ['', Validators.required],
    });
  }

  ngOnInit(): void {}

  public clearForm(): void {
    this.productRegisterForm.reset();
  }

  public registerProduct(): void {
    if (this.productRegisterForm.invalid || this.isRegisterLoading) {
      this.productRegisterForm.markAllAsTouched();
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
          const formValues = this.productRegisterForm.getRawValue();
          let params: product = {};

          Object.entries(formValues).forEach(([key, value]) => {
            if (value) {
              params[`${key}`] = value;
            }
          });

          params.preco_custo = Number(params.preco_custo)
          params.preco_venda = Number(params.preco_custo)
          params.quantidade = Number(params.preco_venda)

          return this.productService.createProduct(params);
        }),
        take(1),
      )
      .subscribe(
        () => {
          this.productRegisterForm.reset();
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

  public onSearchProduct(): void {}

  public updateProduct(): void {}

  public deleteProduct(): void {}
}
