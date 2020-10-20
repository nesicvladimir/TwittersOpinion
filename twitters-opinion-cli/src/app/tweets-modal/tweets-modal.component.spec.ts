import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TweetsModalComponent } from './tweets-modal.component';

describe('TweetsModalComponent', () => {
  let component: TweetsModalComponent;
  let fixture: ComponentFixture<TweetsModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TweetsModalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TweetsModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
