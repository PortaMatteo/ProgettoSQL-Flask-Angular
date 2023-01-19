import { Component} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  url : string = "https://3245-portamatteo-progettosql-re7fqj308cr.ws-eu83.gitpod.io/register/data";
  email:string = '';
  passw:string = '';
  username:string = '';

  constructor(public http: HttpClient,private router: Router) {

  }

  onClickSubmit(data) {
    this.http.post(this.url,{username:data.username,email:data.email,password:data.password}).subscribe(res => {
      if(res){
        this.router.navigate(['/login'])
      }
      else{
        alert('erorre')
      }
    });
  }
}
