import { Component, OnInit, Input } from '@angular/core';
import { Router } from "@angular/router";
import { DatePipe } from '@angular/common'


import { NgbCalendar, NgbDateStruct } from '@ng-bootstrap/ng-bootstrap';

@Component({
    selector: 'app-home-search',
    templateUrl: './home-search.component.html',
    styleUrls: ['./home-search.component.css']
})
export class HomeSearchComponent implements OnInit {

    query: string = '';
    dateNow: NgbDateStruct;
    dateSince: NgbDateStruct = null;
    dateUntil: NgbDateStruct = null;
    useTimeFilter: Boolean = false;
    enableDateUntil: Boolean = false;
    constructor(private router: Router, private calendar: NgbCalendar, public datepipe: DatePipe) { }

    ngOnInit(): void {
    }

    onSubmit() {
        if (this.query === '') {
            alert("Search term can't be empty!");
        } else {
            console.log(this.dateSince);
            if (this.useTimeFilter) {
                    var dateSinceString = this.dateSince.day + '-' + this.dateSince.month + '-' + this.dateSince.year;
                    var dateUntilString = this.dateUntil.day + '-' + this.dateUntil.month + '-' + this.dateUntil.year;
                console.log(dateSinceString);
                this.router.navigateByUrl(`/chart?query=${this.query}&useTimeFilter=${this.useTimeFilter}&dateSince=${dateSinceString}&dateUntil=${dateUntilString}`);
            } else {
                this.router.navigateByUrl(`/chart?query=${this.query}&useTimeFilter=${this.useTimeFilter}`);
            }
        }
    }

    selectToday() {
        return this.dateNow = this.calendar.getToday();
    }
    selectLastWeekDay() {
        var date = new Date();
        var lastWeekDay = new Date(date.getTime() - (6 * 24 * 60 * 60 * 1000));
        var ngbDateStruct = { day: lastWeekDay.getDate(), month: lastWeekDay.getMonth() + 1, year: lastWeekDay.getFullYear() };
        console.log(ngbDateStruct)
        return ngbDateStruct;
    }
    setSinceDate(newDate: NgbDateStruct) {
        this.dateSince = newDate;
        this.enableDateUntil = true;
    }
    setUntilDate(newDate: NgbDateStruct) {
        this.dateUntil = newDate;
    }
}
