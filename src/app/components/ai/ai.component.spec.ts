import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AiCompComponent } from './ai-comp.component';

describe('AiCompComponent', () => {
  let component: AiCompComponent;
  let fixture: ComponentFixture<AiCompComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AiCompComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AiCompComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
