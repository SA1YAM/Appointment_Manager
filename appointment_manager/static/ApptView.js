import FetchUrl from "./FetchUrl.js"
import Header from "./Header.js"

// appointment view 

export default {
	template: `
	<div>
		<navigation></navigation>
		<br><br>
		<div id="app" class="container text-center">
			<div class="row">
					<div class="card border-dark mb-3">
						<div class="card-body text-start">
							<div class="row">
								<div class="col">
									<h5 class="card-title">{{appt.title}}</h5>
									<small class="fw-semibold text-secondary">Scheduled On: {{appt.scheduled_time}}</small>
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
	`,
	
	components:{
		"navigation": Header 
	},
	
	data: function() {
		return {
			appt: {},
		}
	},
	
	mounted: function() {
		
		console.log(this.other_user)
		
		FetchUrl(`http://127.0.0.1:5000/api/appointment/${this.$route.params.apptId}`, {
			method: 'get',
			headers: {
				'Content-Type': 'appication/json',
//				'Authentication-Token': localStorage.getItem('auth-token'),
			},
		})
		.then((data) => {
			console.log(data)
			this.appt = data
		}).catch((err) => {
		console.log(err)
		})
	},
	
}
