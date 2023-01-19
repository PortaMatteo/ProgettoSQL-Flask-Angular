import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent {
  url:string = "https://3245-portamatteo-progettosql-tfawahbl1zv.ws-eu83.gitpod.io/modify"
  id = sessionStorage.getItem('id');
  username = sessionStorage.getItem('username');
  email = sessionStorage.getItem('email');
  constructor(public http: HttpClient,private router: Router) {
    if (sessionStorage.getItem('id') == null){
      this.router.navigate(['/home'])
    }
  }
  onClickSubmit(data) {
    this.http.post(this.url,{id:sessionStorage.getItem('id'),email:data.email,username:data.username}).subscribe(res => {
    });
  }
  
  logout(){
    sessionStorage.clear()
    if (sessionStorage.getItem('id') == null){
      this.router.navigate(['/home'])
    }
  }
}
