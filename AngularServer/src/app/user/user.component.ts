import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent {
  url:string = "https://3245-portamatteo-progettosql-s4pyv9a7xfc.ws-eu83.gitpod.io/modify"
  id = sessionStorage.getItem('id');
  username = sessionStorage.getItem('username');
  email = sessionStorage.getItem('email');
  constructor(public http: HttpClient,private router: Router) {
    if (sessionStorage.getItem('id') == null){
      this.router.navigate(['/home'])
    }
  }
  onClickSubmit(data) {
    this.http.post(this.url,{id:sessionStorage.getItem('id'),username:data.username}).subscribe(res => {
      if(res){
        console.log(data.username)
        sessionStorage.setItem('username',data.username)
        window.location.reload()
      }
      else{
        alert('erorre')
        window.location.reload()
      }
    });
  }
  
  logout(){
    sessionStorage.clear()
    if (sessionStorage.getItem('id') == null){
      this.router.navigate(['/home'])
    }
  }

}
