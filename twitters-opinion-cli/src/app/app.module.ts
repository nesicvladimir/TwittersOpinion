import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SearchTweetsComponent } from './search-tweets/search-tweets.component';
import { HomeSearchComponent } from './home-search/home-search.component';
import { HeaderComponent } from './header/header.component';
import { FormsModule }   from '@angular/forms';
import { NgxSpinnerModule } from "ngx-spinner";  
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { TweetsModalComponent } from './tweets-modal/tweets-modal.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { TopSearchesComponent } from './top-searches/top-searches.component';
import { LiveTestModelComponent } from './live-test-model/live-test-model.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { DatePipe } from '@angular/common';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ChartsModule } from 'ng2-charts/ng2-charts';
import { MDBBootstrapModule } from 'angular-bootstrap-md';
 import { OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime';


@NgModule({
  declarations: [
    AppComponent,
    SearchTweetsComponent,
    HomeSearchComponent,
    HeaderComponent,
    TweetsModalComponent,
    TopSearchesComponent,
    LiveTestModelComponent,
    DashboardComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    FormsModule,
    NgxSpinnerModule,
    BrowserAnimationsModule,
    NgbModule,
    FontAwesomeModule,
    MDBBootstrapModule.forRoot(),
    ChartsModule,
    OwlDateTimeModule,
    OwlNativeDateTimeModule
  ],
  providers: [DatePipe],
  entryComponents: [
    SearchTweetsComponent,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
