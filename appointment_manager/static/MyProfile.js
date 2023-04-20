import FetchUrl from "./FetchUrl.js"
import Header from "./Header.js"

//dashboard view of application
export default {
	template: `
	<div>
		<navigation></navigation>
		<br><br>
		<div id="app" class="container text-center ">
			<div class="row">
				<div class="col text-secondary text-end">
					<h5 class="card-title">Total Appointments : {{ current_user.total_appointments }}</h5>
				</div>			
			</div>
			
			<br><br><br>
			<div class="row">
				<div class="col text-start">
					<h3 class="card-title">My Appointments:</h3>
				</div>			
			</div>
			
			<br><br>
			<div class="row justify-content-center" v-if="current_user.appointments.length > 0">
				<div class="col text-end mb-3">
					  <button type="button" class="btn btn-primary btn-lg mb-3" @click="export_csv" >Export</button>
				</div>
				<div class="row row-cols-3">
					<div class="col" v-for="appt in current_user.appointments">
						<div class="card border-dark mb-3" style="width: 20rem;"> 
						
							<div class="card-body text-start">
								<div class="row">
									<div class="col">
										<h6 class="card-title"><router-link :to="{ name: 'ApptView', params: {apptId: appt.appointment_id } }" class="link-dark" >{{appt.title}}</router-link></h6>
										<small class="fw-semibold text-secondary" >Scheduled On: {{appt.scheduled_time}}</small>
									</div>
									<div class="col">
										<div class="dropdown card-title text-end">
											  <button class="btn btn-secondary btn-sm text-bg-light" type="button" data-bs-toggle="dropdown" aria-expanded="false">
												⋮
											  </button>
											  <ul class="dropdown-menu">
												<li><router-link :to="{ name: 'EditAppt' , query: { appointmentId: appt.appointment_id, title: appt.title, client: appt.client, remarks: appt.remarks, scheduled_time: appt.scheduled_time }}" class="dropdown-item" >Edit</router-link></li>
												<router-link :to="{ name: 'DeleteAppt' , params: {appointmentId: appt.appointment_id}}" class="dropdown-item" role="button" >Delete</router-link>
											  </ul>
										</div>
									</div>
								</div>
								<br>
								
								<br> <br>
								<p class="card-text">Remarks: {{appt.remarks}}</p>
									
							</div>
							<div class="card-footer">
								<div class="row">
									<div class="col">
										<small class="fw-semibold text-success">{{appt.client}}</small>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div class="row justify-content-center" v-else> 
				<h5 class="text-secondary">You have not created any appointments so far. please create appointments</h5>
			</div>
		</div>
	</div>
	`,
	
	components:{
		"navigation": Header 
	},
	
	data: function() {
		return {
			current_user: {},
		}
	},
	
	methods: {
		export_csv: function(){
			FetchUrl("http://127.0.0.1:5000/api/export", {
				method: 'get',
				headers: {
					'Content-Type': 'appication/json',
//					'Authentication-Token': localStorage.getItem('auth-token'),
				},
			})
			.then((data) => {
				console.log(data)
				alert(data.message)
			}).catch((err) => {
			console.log(err)
			})	
		},
	},
	
	mounted: function() {
		
		console.log(this.current_user)
		
		FetchUrl("http://127.0.0.1:5000/api/myprofile", {
			method: 'get',
			headers: {
				'Content-Type': 'appication/json',
//				'Authentication-Token': localStorage.getItem('auth-token'),
			},
		})
		.then((data) => {
			console.log(data)
			this.current_user = data
		}).catch((err) => {
		console.log(err)
		})
	},
	
	updated: function() {
		let apptNames = []
		if(this.current_user.appointments.length > 0){
			for (let appt of this.current_user.appointments){
				apptNames.push(appt.title)
			}
			console.log(apptNames)
			sessionStorage.setItem("apptNames", JSON.stringify(apptNames))
		} else {
			sessionStorage.removeItem("apptNames")
		}
		
	},
	
}