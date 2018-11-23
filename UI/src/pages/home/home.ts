import { Component } from '@angular/core';
import { NavController } from 'ionic-angular';

import { HttpClient } from '@angular/common/http';
import { RestProvider } from '../../providers/rest/rest';
@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {
  message:string;
  bdisplay:boolean = true;
  connect:boolean = false;
  constructor(public navCtrl: NavController, public http: HttpClient, public restProvider: RestProvider) {

  }
  initiateSpeech() {
    var _this = this;
    console.log("API hit");
    this.message= "Connecting ....";
    this.bdisplay = false;
    this.connect = true;
    this.restProvider.requestData();
      console.log("API called");
    setTimeout(function(){ _this.message = "Connected";
    _this.connect = false}, 5000);
  }
  cancel(){
  console.log("cancelled");
    this.message= "";
    this.bdisplay = true;
    this.connect = false;
  }
}
