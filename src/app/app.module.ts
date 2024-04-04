import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatIconModule } from '@angular/material/icon';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BodyComponent } from './sidebar/body/body.component';
import { SidenavComponent } from './sidebar/sidenav/sidenav.component';
import { SettingsComponent } from './components/settings/settings.component';
import { SideNavUtilComponent } from './sidebar/side-nav-util/side-nav-util.component';
import { HomeComponent } from './components/home/home.component';
import { AllCamerasComponent } from './components/all-cameras/all-cameras.component';
import { SelectedCameraComponent } from './components/selected-camera/selected-camera.component';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  declarations: [
    AppComponent,
    BodyComponent,
    SidenavComponent,
    SettingsComponent,
    SideNavUtilComponent,
    HomeComponent,
    AllCamerasComponent,
    SelectedCameraComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatIconModule,
    HttpClientModule,
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
