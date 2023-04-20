import Search from "./Search.js"
import MyProfile from "./MyProfile.js"
import CreateAppt from "./CreateAppointment.js"
import EditAppt from "./EditAppointment.js"
import Logout from "./Logout.js"
import DeleteAppt from "./DeleteAppointment.js"
import ApptView from "./ApptView.js"
import DeleteUser from "./DeleteUser.js"
import ChangePassword from "./ChangePassword.js"

// defining the router for SPA functionality

const routes = [
	{path: "/",name:"MyProfile", component: MyProfile},
	{path: "/signout",name:"Logout", component: Logout},
	{path: "/post/create", name:"CreateAppt", component: CreateAppt},
	{path: "/post/edit", name:"EditAppt", component: EditAppt},
	{path: "/search", name:"Search", component: Search},
	{path: "/post/delete/:appointmentId", name:"DeleteAppt", component: DeleteAppt},
	{path: "/appointmentview/:apptId", name:"ApptView", component: ApptView},
	{path: "/deleteuser", name:"DeleteUser", component: DeleteUser},
	{path: "/changepassword", name:"ChangePassword", component: ChangePassword},
]


export default new VueRouter({
	routes: routes
})