import FetchUrl from "./FetchUrl2.js"
import checkPostForm from "./CheckPostForm.js"
import Header from "./Header.js"

// creates the Appointment
 
export default{
	template: `
		<div>
			<navigation></navigation>
			<br><br>
			<div class = "px-4 mt-4 container-text-center">
				<h1 class = "ms-1 px-2">Create Appointment</h1>
				<br><br>
				<div id="create-card-form" class="ms-1 row g-3 align-items-center fs-5">
				  <div class="col-10">
					<label for="exampleFormControlInput1" class="form-label">Title</label>
					<input type="text" name = "title" required class="form-control" v-model="formData.title" maxlength="20">
					<div id="textHelpBlock" class="form-text">
						 Appointment Title should be less than 20 characters and should not match with any other Appointment Title within selected list.
					</div>
				  </div>
				  <div class="col-10" >
					  <label for="exampleFormControlTextarea1" class="form-label">Client</label>
					  <textarea name = "caption" required class="form-control" rows="3" v-model="formData.client"></textarea>
				  </div>
				  <div class="col-10 mb-3" >
					  <label for="exampleFormControlTextarea1" class="form-label">Remarks</label>
					  <textarea name = "caption" required class="form-control" rows="3" v-model="formData.remarks"></textarea>
				  </div>
				  <div class="row mb-3">
					  <div class="col-4">
						<label for="exampleFormControlInput1" class="form-label">Date of Appointment</label>
						<input type="date" id="birthday" name="deadline" class="form-control text-center" v-model="formData.date" required>
						<div id="birthdayHelpBlock" class="form-text">
							 scheduled date should be on or after today's date.
						</div>
					  </div>
					  <div class="col-4 mb-3">
						<label for="exampleFormControlInput2" class="form-label">Time of Appointment</label>
						<input type="time" id="appt" name="timeline" class="form-control text-center" v-model="formData.time" required>
					  </div>
				  </div>
				  <div>
					<button @click="createAppntmnt" class="btn btn-primary">Submit</button>
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
			formData: {
				title: null,
				client: null, 
				remarks: null,
				date: null,
				time: null,
			},
			errors: [],
		}
	},
	
	methods: {
		createAppntmnt: function() {
			console.log(this.formData)
			let checkList = JSON.parse(sessionStorage.getItem("apptNames"))
			console.log(checkList)
			this.errors = checkPostForm(this.formData)
			if(checkList && checkList.includes(this.formData.title)){
				this.errors.push("title already exists for some other appointment please change the title")
			}
			if(this.errors.length > 0){
				return
			}
			FetchUrl('http://127.0.0.1:5000/api/appointment', {
				method: 'post',
				headers: {
				'Content-Type': 'application/json',
				},
				body: JSON.stringify(this.formData),
			})
			.then((data) => {
			  console.log(data)
			  this.$router.push({name: 'MyProfile'})
			})
			.catch((err) => {
//				alert(err)
				this.errors.push(err)
			})
		},
	},
	
}