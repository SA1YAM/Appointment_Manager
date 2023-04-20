import FetchUrl from "./FetchUrl2.js"
import Header from "./Header.js"

export default{
	template: `
		<div>
			<navigation></navigation>
			<br><br>
			<div id="app" class = "px-4 mt-4">
				<h1>Change Password</h1>
				<br>
				<div class="row mb-3">
					<p class="text-xl-start fs-5"> Are you sure you want to change your password. Please fill the below form for authentication if you want to change your password. </p>
				</div>
				<br>
				<div class ="row g-3 fs-5">
					<div class="mb-3">
						<label for="exampleInputEmail1" class="form-label">Email address:</label>
						<input type="email" name = "email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" v-model="formData.email" required  />
						<div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
					</div>
					<div class="mb-3 .w-50 form-group">
						<label for="inputPassword5" class="form-label">Current Password</label>
						<input type="password" name = "password" id="inputPassword5" class="form-control" aria-describedby="passwordHelpBlock" v-model="formData.oldPassword" required />
						<div id="passwordHelpBlock" class="form-text">
						  Your password must be 5-20 characters long and must not contain spaces.
						</div>
					</div>
					<div class="mb-3 .w-50 form-group">
						<label for="inputPassword6" class="form-label">New Password</label>
						<input type="password" name = "password" id="inputPassword6" class="form-control" aria-describedby="passwordHelpBlock" v-model="formData.newPassword" required />
						<div id="passwordHelpBlock" class="form-text">
						  Your password must be 5-20 characters long and must not contain spaces.
						</div>
					</div>
					
					<div>
						<button @click="changePassword" class="btn btn-primary">Delete</button>
					</div>
					<div class="text-danger">
					  <p v-if="errors.length > 0">
						<b class="card-title">Please correct the following error(s):</b>
						<ul>
						  <li v-for="error in errors">{{ error }}</li>
						</ul>
					  </p>
					</div>
				</div>
			</div>
		</div>
	`,
	
	components:{
		"navigation": Header 
	},
	
	data: function(){
		return{	
			formData:{
				email: null,
				oldPassword: null,
				newPassword: null,
			},
			errors: [],
		}
	},
	
  methods: {
    changePassword: function() {
		  FetchUrl('http://127.0.0.1:5000/api/user', {
			method: 'put',
			headers: {
			  'Content-Type': 'application/json',
			},
			body: JSON.stringify(this.formData),
		  })
		  .then((data) => { 
			  console.log(data)
			  this.$router.push({name: 'Logout'})
		  })
		  .catch((err) => {
			  this.errors = err.message.split(",")
			  console.log(typeof err.message)
		  })
    },
  },
}