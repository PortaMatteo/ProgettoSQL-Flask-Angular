import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlaylistDotComponent } from './playlist-dot.component';

describe('PlaylistDotComponent', () => {
  let component: PlaylistDotComponent;
  let fixture: ComponentFixture<PlaylistDotComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PlaylistDotComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PlaylistDotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
