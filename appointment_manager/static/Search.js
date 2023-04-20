import FetchUrl from "./FetchUrl.js"
import Header from "./Header.js"

// search template which search out the appointments which matches with the starting expression

export default{
	template: `
		<div>
			<navigation></navigation>
			<br><br>	
			<div id="app" class="container text-center ">
			
				<div class="row">
					<div class="col text-start">
						<h3>Search</h3>
					</div>
				</div>
				
				<br><br>

				<div class="row justify-content-center">
					<p class="input-group">
					  <input type="search" class="form-control rounded" placeholder="Search" aria-label="Search" aria-describedby="search-addon" v-model="content" />
					  <button type="button" ref="searchBtn" class="btn btn-outline-primary" data-bs-toggle="collapse" data-bs-target="#collapseExample" aria-expanded="false" aria-controls="collapseExample" @click="search" >
						SEARCH
					  </button>
					</p>
					<div class="collapse" id="collapseExample">
					  <div class="card card-body">
						<div class="row justify-content-center" v-if="searchlist.length === 0">
							<h5 class="text-secondary">There are no appointments matching this title</h5>
						</div>
						<div class="row" v-else>
							<ul class="list-group">
							  <li class="list-group-item d-flex justify-content-between align-items-center" v-for="appt in searchlist">
							  <h6 class="card-title"> {{ appt.title }} </h6>
								<button class="badge bg-primary rounded-pill" @click="view(appt.appointment_id)">View</button>
							  </li>
							</ul>
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
	
	data: function(){
		return{
			content: "",
			apptlist: [],
			searchlist: [],
			current_user: {},
		}
	},
	
	methods: {
		search: function(){
			this.searchlist = []
			for(let i of this.apptlist){
				let rege = "^" + this.content
				let regex = new RegExp(rege,)
				console.log(regex)
				if(regex.test(i.title)){
					this.searchlist.push(i)
				}
				
			}
			console.log("searchlist",this.searchlist)	
		},
		
		view: function(appt_Id){
			this.$refs.searchBtn.click()
			this.$router.push({ name: 'ApptView', params:{ apptId: appt_Id } })
		},
		
	},
	
	mounted: function(){
		this.current_user = JSON.parse(sessionStorage.getItem("current_user"))
		FetchUrl("http://127.0.0.1:5000/api/search", {
			method: 'get',
			headers: {
				'Content-Type': 'appication/json',
//				'Authentication-Token': localStorage.getItem('auth-token'),
			},
		})
		.then((data) => {
			console.log(data)
			this.apptlist = data
		}).catch((err) => {
		console.log(err)
		})
	},
}