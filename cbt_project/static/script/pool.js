class pool{

	constructor(x){
		this.exit_count = x;
	}

	add_count(){
		this.exit_count += 1;
	}

	get_count(){
		return this.exit_count;
	}
}
