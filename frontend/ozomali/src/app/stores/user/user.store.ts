import { Injectable } from '@angular/core';
import { Store, StoreConfig } from '@datorama/akita';

export interface UserState {
  userInfo: any;
  token: string;
}

export function createInitialState(): UserState {
  return {
    userInfo: {},
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
