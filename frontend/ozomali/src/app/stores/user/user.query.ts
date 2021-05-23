import { Injectable } from '@angular/core';
import { Query } from '@datorama/akita';
import { UserStore, UserState } from './user.store';

@Injectable({ providedIn: 'root' })
export class UserQuery extends Query<UserState> {
  isAuthenticated$ = this.select('isAuthenticated');
  user$ = this.select('user');
  token$ = this.select('token');

  constructor(protected store: UserStore) {
    super(store);
  }

  get token() {
    return this.getValue().token;
  }
}
