import { Injectable } from '@angular/core';
import { Store, StoreConfig } from '@datorama/akita';

export interface UserState {
  key: string;
  isAuthenticated: boolean;
  user: any;
  token: string;
}

export function createInitialState(): UserState {
  return {
    key: '',
    isAuthenticated: false,
    user: {},
    token: '',
  };
}

@Injectable({ providedIn: 'root' })
@StoreConfig({ name: 'user', resettable: true })
export class UserStore extends Store<UserState> {
  constructor() {
    super(createInitialState());
  }
}
