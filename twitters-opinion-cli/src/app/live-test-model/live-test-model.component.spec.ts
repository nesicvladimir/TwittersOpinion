import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LiveTestModelComponent } from './live-test-model.component';

describe('LiveTestModelComponent', () => {
  let component: LiveTestModelComponent;
  let fixture: ComponentFixture<LiveTestModelComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LiveTestModelComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LiveTestModelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
