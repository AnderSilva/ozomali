import { Component } from '@angular/core';

@Component({
  selector: 'app-users-screen',
  templateUrl: './users-screen.component.html',
  styleUrls: ['./users-screen.component.scss'],
})
export class UsersScreenComponent {
  public users: any;
  public resultUser: any;
  public shouldSearch: boolean;

  constructor() {
    this.shouldSearch = true;
  }

  public setUsers(users: any): void {
    this.users = users;
  }

  public loadUser(user: any): void {
    this.resultUser = user;
    this.shouldSearch = false;
    this.users = undefined;
  }

  public clearSearch(): void {
    this.shouldSearch = true;
  }
}
