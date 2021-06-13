import { Injectable } from '@angular/core';
import { Query } from '@datorama/akita';
import { UserStore, UserState } from './user.store';

@Injectable({ providedIn: 'root' })
export class UserQuery extends Query<UserState> {
  isAuthenticated$ = this.select(state => !!state.token);
  userInfo$ = this.select('userInfo');
  token$ = this.select('token');

  constructor(protected store: UserStore) {
    super(store);
  }

  get token(): string {
    return this.getValue().token;
  }

  get userInfo(): any {
    return this.getValue().userInfo;
  }
}
