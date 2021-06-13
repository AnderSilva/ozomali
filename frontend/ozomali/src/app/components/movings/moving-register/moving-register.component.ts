import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Observable } from 'rxjs';
import { filter, map, startWith, switchMap, take } from 'rxjs/operators';
import { MovingsService } from 'src/app/services/movings/movings.service';
import { NotificationService } from 'src/app/services/notification/notification.service';
import { UserQuery } from 'src/app/stores/user';

@Component({
  selector: 'app-moving-register',
  templateUrl: './moving-register.component.html',
  styleUrls: ['./moving-register.component.scss'],
})
export class MovingRegisterComponent implements OnInit {
  public productMovingForm: FormGroup;
  public isMovingLoading: boolean;

  @Input() public isSearch: boolean;
  @Output() public results = new EventEmitter<any>();

  @Input() public products: any;
  @Input() public productNames: string[];

  public filteredProducts: Observable<string[]>;
  public product: FormControl;

  public userInfo$: Observable<any>;

  constructor(
    private formBuilder: FormBuilder,
    private notifications: NotificationService,
    private movingsService: MovingsService,
    private userQuery: UserQuery,
  ) {
    this.product = new FormControl('', Validators.required);

    this.productMovingForm = this.formBuilder.group({
      local_estoque: ['', Validators.required],
      tipo_movimentacao: ['', Validators.required],
      quantidade: ['', Validators.required],
      produto_id: ['', Validators.required],
      preco_total: ['', Validators.required],
    });

    this.userInfo$ = this.userQuery.userInfo$;
  }

  ngOnInit(): void {
    this.filteredProducts = this.product.valueChanges.pipe(
      startWith(''),
      map(value => this.filterProducts(value)),
    );
  }

  private filterProducts(value: string): string[] {
    const filterValue = value?.toLowerCase();

    return this.productNames.filter(option => option?.toLowerCase().includes(filterValue));
  }

  public productChosen(productName: string): void {
    const matchProduct = this.products.find((product: any) => product.nome === productName);

    this.productMovingForm.get('produto_id').setValue(matchProduct.id);
  }

  public clearForm(): void {
    this.productMovingForm.reset();
    this.product.reset();
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
    if (this.productMovingForm.invalid || this.product.invalid || this.isMovingLoading) {
      this.productMovingForm.markAllAsTouched();
      this.product.markAsTouched();
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

          formValues.produto_id = Number(formValues.produto_id);
          formValues.quantidade = Number(formValues.quantidade);

          if (formValues.tipo_movimentacao === 'S') {
            delete formValues.preco_total;
          }

          return this.movingsService.registerMoving(formValues);
        }),
        take(1),
      )
      .subscribe(
        response => {
          this.productMovingForm.reset();
          this.product.reset();
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
    if (this.product.invalid || this.isMovingLoading) {
      this.product.markAllAsTouched();
      return;
    }

    this.isMovingLoading = true;

    const id = Number(this.productMovingForm.get('produto_id').value);

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
