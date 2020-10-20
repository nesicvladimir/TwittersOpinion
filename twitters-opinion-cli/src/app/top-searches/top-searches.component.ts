import { SearchTerm } from './../shared/models/search-term.model';
import { TwitterSearchService } from './../shared/services/twitter-search.service';
import { Component, OnInit } from '@angular/core';

@Component({
    selector: 'app-top-searches',
    templateUrl: './top-searches.component.html',
    styleUrls: ['./top-searches.component.css']
})
export class TopSearchesComponent implements OnInit {

    topSearches: SearchTerm[] = [];

    constructor(private service: TwitterSearchService) { }

    ngOnInit(): void {
         this.service.getTopSearches().subscribe(
            res => {
                this.topSearches = res;
                console.log(this.topSearches);
            },
            err => {
                console.log(err);
            }
        );
    }

}
