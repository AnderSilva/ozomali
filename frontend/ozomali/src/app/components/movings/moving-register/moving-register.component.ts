import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { filter, switchMap, take } from 'rxjs/operators';
import { MovingsService } from 'src/app/services/movings/movings.service';
import { NotificationService } from 'src/app/services/notification/notification.service';

@Component({
  selector: 'app-moving-register',
  templateUrl: './moving-register.component.html',
  styleUrls: ['./moving-register.component.scss'],
})
export class MovingRegisterComponent implements OnInit {
  public productMovingForm: FormGroup;
  public productMovingSearchForm: FormGroup;
  public isMovingLoading: boolean;

  @Input() public isSearch: boolean;
  @Output() public results = new EventEmitter<any>();

  constructor(
    private formBuilder: FormBuilder,
    private notifications: NotificationService,
    private movingsService: MovingsService,
  ) {
    this.productMovingForm = this.formBuilder.group({
      local_estoque: ['', Validators.required],
      tipo_movimentacao: ['', Validators.required],
      quantidade: ['', Validators.required],
      produto_id: ['', Validators.required],
      preco_total: ['', Validators.required],
    });

    this.productMovingSearchForm = this.formBuilder.group({
      id: ['', Validators.required],
    });
  }

  ngOnInit(): void {}

  public clearForm(): void {
    // this.clearSearch.emit();
    this.productMovingForm.reset();
    // this.product = undefined;
  }

  public updateValidity(value: string): void {
    const input = this.productMovingForm.get('preco_total');

    switch (value) {
      case 'E':
        input.setValidators(Validators.required);
        break;
      case 'S':
        input.setValidators(null);
        break;
    }

    input.updateValueAndValidity();
  }

  public registerMoving(): void {
    if (this.productMovingForm.invalid || this.isMovingLoading) {
      this.productMovingForm.markAllAsTouched();
      return;
    }

    const confirmationModal = this.notifications.confirmationModal(
      'Você realmente quer salvar esse movimentação?',
      'Sim',
      'Não',
    );

    confirmationModal
      .afterClosed()
      .pipe(
        filter(confirmation => confirmation === true),
        switchMap(() => {
          this.isMovingLoading = true;
          const formValues = this.productMovingForm.getRawValue();

          formValues.preco_total = Number(formValues.preco_total);
          formValues.produto_id = Number(formValues.produto_id);
          formValues.quantidade = Number(formValues.quantidade);

          return this.movingsService.registerMoving(formValues);
        }),
        take(1),
      )
      .subscribe(
        response => {
          this.productMovingForm.reset();
          this.isMovingLoading = false;
          this.notifications.feedbackModal(response);
        },
        response => {
          this.isMovingLoading = false;
          this.notifications.feedbackModal(response);
        },
      );
  }

  public onSearchProductMovings(): void {
    if (this.productMovingSearchForm.invalid || this.isMovingLoading) {
      this.productMovingSearchForm.markAllAsTouched();
      return;
    }

    this.isMovingLoading = true;

    const id = this.productMovingSearchForm.get('id').value;

    this.movingsService
      .getMovings(id)
      .pipe(take(1))
      .subscribe(
        movings => {
          this.isMovingLoading = false;
          this.results.emit(movings.data);
        },
        response => {
          this.isMovingLoading = false;
          this.notifications.feedbackModal(response);
        },
      );
  }

  public getMovings(): void {
    if (this.isMovingLoading) {
      return;
    }

    this.isMovingLoading = true;

    this.movingsService
      .listAllMovings()
      .pipe(take(1))
      .subscribe(
        products => {
          this.isMovingLoading = false;
          this.results.emit(products.data);
        },
        response => {
          this.isMovingLoading = false;
          this.notifications.feedbackModal(response);
        },
      );
  }
}
