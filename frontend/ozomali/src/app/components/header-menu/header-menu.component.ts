import { Component, EventEmitter, Output } from '@angular/core';
import { Observable } from 'rxjs';
import { UserQuery } from 'src/app/stores/user';

@Component({
  selector: 'app-header-menu',
  templateUrl: './header-menu.component.html',
  styleUrls: ['./header-menu.component.scss'],
})
export class HeaderMenuComponent {
  @Output() public shouldLogout: EventEmitter<void> = new EventEmitter();
  user$: Observable<any>;

  constructor(private userQuery: UserQuery) {
    this.user$ = this.userQuery.user$;
  }

  public logout(): void {
    this.shouldLogout.emit();
  }
}
