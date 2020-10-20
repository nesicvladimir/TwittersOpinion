import { TestBed } from '@angular/core/testing';

import { TwitterSearchService } from './twitter-search.service';

describe('TwitterSearchService', () => {
  let service: TwitterSearchService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TwitterSearchService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
