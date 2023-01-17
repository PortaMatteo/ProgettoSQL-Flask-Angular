import { Component } from '@angular/core';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent {
  id = sessionStorage.getItem('id');
  username = sessionStorage.getItem('username');
  email = sessionStorage.getItem('email');
}
