import { TestBed } from '@angular/core/testing';

import { MovingsService } from './movings.service';

describe('MovingsService', () => {
  let service: MovingsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MovingsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
