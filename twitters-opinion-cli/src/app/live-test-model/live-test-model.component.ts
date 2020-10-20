import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { TwitterSearchService } from '../shared/services/twitter-search.service';

@Component({
    selector: 'app-live-test-model',
    templateUrl: './live-test-model.component.html',
    styleUrls: ['./live-test-model.component.css']
})
export class LiveTestModelComponent implements OnInit {

    query: string = '';
    score: number;
    imgSrc: string = '';
    label: string = '';
    constructor(private service: TwitterSearchService) { }

    ngOnInit(): void {
    }

    onSubmit() {
        console.log(this.query);
        this.service.getLiveTest(this.query).subscribe(
            res => {
                this.score = res;
                console.log(this.score);
                if (this.score >= 0.80) {
                    this.imgSrc = "assets/img/very-positive.PNG";
                    this.label = 'Very positive';
                } else if (this.score >= 0.60 && this.score < 0.80) {
                    this.imgSrc = "assets/img/positive.PNG";
                    this.label = 'Positive';
                } else if (this.score >= 0.40 && this.score < 0.60) {
                    this.imgSrc = "assets/img/neutral.PNG";
                    this.label = 'Neutral';
                } else if (this.score >= 0.20 && this.score < 0.40) {
                    this.imgSrc = "assets/img/negative.PNG";
                    this.label = 'Negative';
                } else {
                    this.imgSrc = "assets/img/very-negative.PNG";
                    this.label = 'Very negative';
                }
            },
            err => {
                console.log(err);
            }
        );
    }

}
