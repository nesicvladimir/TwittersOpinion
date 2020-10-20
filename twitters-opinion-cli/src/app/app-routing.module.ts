import { DashboardComponent } from './dashboard/dashboard.component';
import { LiveTestModelComponent } from './live-test-model/live-test-model.component';
import { SearchTweetsComponent } from './search-tweets/search-tweets.component';
import { HomeSearchComponent } from './home-search/home-search.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';


const routes: Routes = [
    {
        path: '',
        redirectTo: '/search',
        pathMatch: 'full'
    },
    {
        path: 'search',
        component: HomeSearchComponent
    },
    {
        path: 'chart',
        component: SearchTweetsComponent
    },
    {
        path: 'liveTest',
        component: LiveTestModelComponent
    },
    {
        path: 'dashboard',
        component: DashboardComponent
    }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }
