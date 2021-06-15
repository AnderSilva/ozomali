import { Component, EventEmitter, Input, OnInit, Output, SimpleChanges } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Subject } from 'rxjs';
import { filter, switchMap, take } from 'rxjs/operators';
import { NotificationService } from 'src/app/services/notification/notification.service';
import { UsersService } from 'src/app/services/users/users.service';

@Component({
  selector: 'app-user-register',
  templateUrl: './user-register.component.html',
  styleUrls: ['./user-register.component.scss'],
})
export class UserRegisterComponent implements OnInit {
  private readonly unsubscribe$: Subject<void> = new Subject<void>();
  public isRegisterLoading: boolean;
  public userRegisterForm: FormGroup;
  public userSearchForm: FormGroup;
  public mask: string;

  @Input() public user: any;
  @Input() public isSearch: boolean;
  @Output() public results = new EventEmitter<any>();
  @Output() public clearSearch = new EventEmitter<any>();

  constructor(
    private formBuilder: FormBuilder,
    private usersService: UsersService,
    private notifications: NotificationService,
  ) {
    this.isRegisterLoading = false;

    this.userRegisterForm = this.formBuilder.group({
      login: ['', Validators.required],
      nome: ['', Validators.required],
      senha: ['', Validators.required],
      perfil_id: ['', Validators.required],

      ativo: [''],
      id: [{ value: '', disabled: true }],
    });

    this.userSearchForm = this.formBuilder.group({
      filter: ['', Validators.required],
      status: [''],
      perfil_id: [''],
      param: ['', Validators.required],
    });
  }

  ngOnInit(): void {
    if (this.isSearch) {
      this.userRegisterForm.get('senha').disable();
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.user?.currentValue !== changes.user?.previousValue) {
      this.setUserForm(this.user);
    }
  }

  ngOnDestroy(): void {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  public clearForm(): void {
    this.clearSearch.emit();
    this.userRegisterForm.reset();
    this.user = undefined;
  }

  public updateValidity(value: string): void {
    const paramInput = this.userSearchForm.get('param');
    const statusInput = this.userSearchForm.get('status');
    const accessInput = this.userSearchForm.get('perfil_id');

    switch (value) {
      case 'ativo':
        paramInput.setValidators(null);
        accessInput.setValidators(null);
        statusInput.setValidators(Validators.required);
        break;
      case 'perfil_id':
        paramInput.setValidators(null);
        statusInput.setValidators(null);
        accessInput.setValidators(Validators.required);
        break;
      default:
        statusInput.setValidators(null);
        accessInput.setValidators(null);
        paramInput.setValidators(Validators.required);
        break;
    }

    paramInput.updateValueAndValidity();
    statusInput.updateValueAndValidity();
    accessInput.updateValueAndValidity();
  }

  public updateMask(filterValue: string): void {
    this.userSearchForm.get('param').reset();

    switch (filterValue) {
      case 'id':
        this.mask = '9999999999999';
        break;
      default:
        this.mask = '';
        break;
    }
  }

  public registerUser(): void {
    if (this.userRegisterForm.invalid || this.isRegisterLoading) {
      this.userRegisterForm.markAllAsTouched();
      console.log(this.isSearch);
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
          const formValues = this.userRegisterForm.getRawValue();

          delete formValues.ativo;
          delete formValues.id;

          return this.usersService.createUser(formValues);
        }),
        take(1),
      )
      .subscribe(
        response => {
          this.userRegisterForm.reset();
          this.isRegisterLoading = false;
          this.notifications.feedbackModal(response);
        },
        response => {
          this.isRegisterLoading = false;
          this.notifications.feedbackModal(response);
        },
      );
  }

  public onSearchUser(): void {
    if (this.userSearchForm.invalid || this.isRegisterLoading) {
      this.userSearchForm.markAllAsTouched();
      return;
    }

    const filter = this.userSearchForm.get('filter').value;
    let value: any = this.userSearchForm.get('param').value;
    this.isRegisterLoading = true;

    if (filter === 'id') {
      value = Number(this.userSearchForm.get('param').value);
    }
    if (filter === 'ativo') {
      value = this.userSearchForm.get('status').value;
    }
    if (filter === 'perfil_id') {
      value = this.userSearchForm.get('perfil_id').value;
    }

    this.usersService
      .searchUsers(filter, value)
      .pipe(take(1))
      .subscribe(
        users => {
          this.isRegisterLoading = false;
          this.results.emit(users.data);
        },
        response => {
          this.isRegisterLoading = false;
          this.notifications.feedbackModal(response);
        },
      );
  }

  public setUserForm(user: any): void {
    this.userRegisterForm.get('login').setValue(user.login);
    this.userRegisterForm.get('nome').setValue(user.nome);
    this.userRegisterForm.get('perfil_id').setValue(user.perfil_id);

    this.userRegisterForm.get('id').setValue(user.id);
    this.userRegisterForm.get('ativo').setValue(user.ativo);
  }

  public getUsers(): void {
    if (this.isRegisterLoading) {
      return;
    }

    this.isRegisterLoading = true;

    this.usersService
      .getUsers()
      .pipe(take(1))
      .subscribe(
        users => {
          this.isRegisterLoading = false;
          this.results.emit(users.data);
        },
        response => {
          this.isRegisterLoading = false;
          this.notifications.feedbackModal(response);
        },
      );
  }

  public updateUser(): void {
    if (this.userRegisterForm.invalid || this.isRegisterLoading) {
      this.userRegisterForm.markAllAsTouched();
      return;
    }

    this.isRegisterLoading = true;
    const formValues = this.userRegisterForm.getRawValue();

    delete formValues.senha;
    delete formValues.id;

    this.usersService
      .updateUser(this.user.id, formValues)
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
