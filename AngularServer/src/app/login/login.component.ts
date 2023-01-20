import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  email:string = '';
  passw:string = '';
  url:string = "https://3245-portamatteo-progettosql-s4pyv9a7xfc.ws-eu83.gitpod.io/login/data"
  constructor(public http: HttpClient,private router: Router) {
    if (sessionStorage.getItem('id') != null){
      this.router.navigate(['/home'])
    }
   console.log(sessionStorage.getItem('id'))
  }

  onClickSubmit(data) {
    this.http.post(this.url,{email:data.email,password:data.password}).subscribe(res => {
        sessionStorage.setItem('username',res[0].username)
        sessionStorage.setItem('id',res[0].id)
        sessionStorage.setItem('email',res[0].email)
        this.router.navigate(['/login'])
        if (sessionStorage.getItem('id') != null){
          this.router.navigate(['/home'])
        }
    });
  }
}
