import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SideNavUtilComponent } from './side-nav-util.component';

describe('SideNavUtilComponent', () => {
  let component: SideNavUtilComponent;
  let fixture: ComponentFixture<SideNavUtilComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SideNavUtilComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SideNavUtilComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
