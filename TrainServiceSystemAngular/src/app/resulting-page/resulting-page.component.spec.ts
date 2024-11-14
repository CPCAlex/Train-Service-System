import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResultingPageComponent } from './resulting-page.component';

describe('ResultingPageComponent', () => {
  let component: ResultingPageComponent;
  let fixture: ComponentFixture<ResultingPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ResultingPageComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ResultingPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
