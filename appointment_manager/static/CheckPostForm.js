
export default function CheckPostForm(data){
	let errors = []
	console.log(data)
	if(!data.title){
		errors.push("title is required")
	} else {
		if(data.title.length > 20){
			errors.push("title should be less than 20 characters")
		}
		if (data.title.trim().length < 1){
			errors.push("title cannot contain only whitespaces")
		}
	}
	if(!data.client){
		errors.push("caption is required")
	} else {
		if(data.client.length > 100){
			errors.push("client name should be less than 100 characters")
		}
		if (data.client.trim().length < 1){
			errors.push("client name cannot contain only whitespaces")
		}
	}
	if(!data.remarks){
		errors.push("remarks is required Please enter remarks")
	}
	if(!data.date){
		errors.push("Schedule Date is required Please choose a date")
	}
	if(!data.time){
		errors.push("Schedule time is required Please choose a time")
	}
	return errors
}