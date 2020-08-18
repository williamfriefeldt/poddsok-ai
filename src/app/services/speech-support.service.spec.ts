import { TestBed } from '@angular/core/testing';

import { SpeechSupportService } from './speech-support.service';

describe('SpeechSupportService', () => {
  let service: SpeechSupportService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SpeechSupportService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
