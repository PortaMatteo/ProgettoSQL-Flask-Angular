import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { NgModule } from '@angular/core';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  email:string = '';
  passw:string = '';
  url:string = "https://3245-portamatteo-progettosql-z1qz8oxtg0n.ws-eu82.gitpod.io/login/data"
  constructor(public http: HttpClient) {
  }

  onSubmit(email:string,passw:string){
    this.http.post(this.url,{email:email,password:passw}).subscribe(res => {
      sessionStorage.setItem('email',res[0].email)
      sessionStorage.setItem('username',res[0].username)
      sessionStorage.setItem('id',res[0].id)
      });
  }
}
