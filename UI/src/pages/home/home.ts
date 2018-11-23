import { Component } from '@angular/core';
import { NavController } from 'ionic-angular';

import { HttpClient } from '@angular/common/http';
import { RestProvider } from '../../providers/rest/rest';
@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {

  constructor(public navCtrl: NavController, public http: HttpClient, public restProvider: RestProvider) {

  }
  initiateSpeech() {
    console.log("API hit");
    this.restProvider.requestData();
      console.log("API called");

  }
}
