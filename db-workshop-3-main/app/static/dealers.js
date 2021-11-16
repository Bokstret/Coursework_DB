async function getData() {
    const responce = await fetch(location.protocol + '//' + location.host + location.pathname + 'api/dealers');
    const data = await responce.json();
    console.log(data.dealers);
    return data.dealers
}


class SaleplaceRow extends React.Component {
    constructor (props) {
        super(props);

        this.handleDelete = this.handleDelete.bind(this);
        this.handleSubmitEdited = this.handleSubmitEdited.bind(this);

        this.state = {toggle_edit : false, new_address : this.props.address};
    }


    handleDelete() {
        let formData = new FormData();
        formData.append('id', this.props.id);

        var request = new XMLHttpRequest();
        request.open("DELETE", location.protocol + '//' + location.host + location.pathname + 'api/saleplaces');
        request.send(formData);

        document.location.reload();
    }


    handleToggle() {
        this.setState({
            toggle_edit : !this.state.toggle_edit
        });
    }


    handleAddressChange(e) {
        this.setState({new_address : e.target.value});
    }


    handleSubmitEdited(e) {
        let formData = new FormData();
        formData.append('id', this.props.id);
        formData.append('address', this.state.new_address);

        var request = new XMLHttpRequest();
        request.open("PUT", location.protocol + '//' + location.host + location.pathname + 'api/saleplaces');
        request.send(formData);
    }


    render() {
        const address = this.props.address;

        let to_show;

        if (this.state.toggle_edit) {
            to_show = (
                <form onSubmit={this.handleSubmitEdited}>
                    <div className="d-flex">
                            <input className="form-control form-control-sm" type="text" placeholder="New address" 
                            value={this.state.new_address} onChange={(e) => this.handleAddressChange(e)}/>
                            <input type="submit" className="btn btn-primary btn-sm" value="Edit"/>
                            <button type="button" className="btn btn-danger btn-sm" onClick={() => this.handleToggle()}>Close</button>
                    </div>
                </form>
            );
        } else {
            to_show = (
                <div className='d-flex bd-highlight mb-3'>
                    <div className="mr-auto p-2 bd-highlight">{address}</div>
                    <button className="p-2 btn btn-warning btn-sm" onClick={() => this.handleToggle()}>Edit</button>
                    <button className="p-2 btn btn-danger btn-sm" onClick={this.handleDelete}>Delete</button>
                </div>
            );
        }

        return <tr>
            <td>
                {to_show}
            </td>
        </tr>
    }
}


class DealerRow extends React.Component {
    constructor(props) {
        super(props);
        this.handleAddAddress = this.handleAddAddress.bind(this);
        this.handleCloseAddress = this.handleCloseAddress.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);

        this.handleDelete = this.handleDelete.bind(this);

        this.handleSubmitEdited = this.handleSubmitEdited.bind(this);

        this.state = {add_new: false, new_address: '', new_name : this.props.name};
    }
    
    handleAddAddress() {
        this.setState({add_new: true});
    }

    handleCloseAddress() {
        this.setState({add_new: false});
    }

    handleSubmit(e) {
        let formData = new FormData();
        formData.append('dealer_id', this.props.id);
        formData.append('address', this.state.new_address);

        var request = new XMLHttpRequest();
        request.open("POST", location.protocol + '//' + location.host + location.pathname + 'api/saleplaces');
        request.send(formData);
    }

    handleChange(e) {
        this.setState({new_address: e.target.value});
    }

    handleDelete() {
        let formData = new FormData();
        formData.append('id', this.props.id);

        var request = new XMLHttpRequest();
        request.open("DELETE", location.protocol + '//' + location.host + location.pathname + 'api/dealers');
        request.send(formData);

        document.location.reload();
    }



    handleToggle() {
        this.setState({
            toggle_edit : !this.state.toggle_edit
        });
    }


    handleNameChange(e) {
        this.setState({new_name : e.target.value});
    }


    handleSubmitEdited(e) {
        let formData = new FormData();
        formData.append('id', this.props.id);
        formData.append('name', this.state.new_name);

        var request = new XMLHttpRequest();
        request.open("PUT", location.protocol + '//' + location.host + location.pathname + 'api/dealers');
        request.send(formData);
    }





    render() {
        const name = this.props.name;
        let to_show;
        if (this.state.add_new){
            to_show = (<td>
                <form onSubmit={this.handleSubmit}>
                    <div className="d-flex">
                            <input className="form-control form-control-sm" type="text" placeholder="New address" 
                            value={this.state.new_address} onChange={this.handleChange}/>
                            <input type="submit" className="btn btn-primary btn-sm" value="Add"/>
                            <button type="button" className="btn btn-danger btn-sm" onClick={this.handleCloseAddress}>Close</button>
                    </div>
                </form>
                </td>);
        } else {
            to_show = <button type="button" className="btn btn-info" onClick={this.handleAddAddress}>Add address</button>
        }



        let editing_name;
        if (this.state.toggle_edit) {
            editing_name = (
                <form onSubmit={this.handleSubmitEdited}>
                    <div className="d-flex">
                            <input className="form-control form-control-sm" type="text" placeholder="New address" 
                            value={this.state.new_name} onChange={(e) => this.handleNameChange(e)}/>
                            <input type="submit" className="btn btn-primary btn-sm" value="Edit"/>
                            <button type="button" className="btn btn-danger btn-sm" onClick={() => this.handleToggle()}>Close</button>
                    </div>
                </form>
            );
        } else {
            editing_name = (
                <div className='d-flex bd-highlight mb-3'>
                    <div className="mr-auto p-2 bd-highlight">{name}</div>
                    <button className="p-2 btn btn-warning btn-sm" onClick={() => this.handleToggle()}>Edit</button>
                    <button className="p-2 btn btn-danger btn-sm" onClick={this.handleDelete}>Delete</button>
                </div>
            );
        }


        return <tr>
            <th>
                {editing_name}
            </th>



                <td>
                <table className="table">
                <tbody>
                    {this.props.saleplaces.map(el => (
                        <SaleplaceRow address={el.address} key={el.saleplace_id} id={el.saleplace_id}/>
                    ))}
                    <tr>
                        {to_show}
                    </tr>
                </tbody>
            </table>
            </td>
        </tr>
    }
}


class DealersData extends React.Component {
    constructor(props) {
        super(props);
        this.handleAddDealer = this.handleAddDealer.bind(this);
        this.handleCloseDealer = this.handleCloseDealer.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.state = {dealers: [], add_new: false, new_dealer: ''};
    }
    
    handleAddDealer() {
        this.setState({add_new: true});
    }

    handleCloseDealer() {
        this.setState({add_new: false});
    }

    handleSubmit(e) {
        let formData = new FormData();
        formData.append('name', this.state.new_dealer);

        var request = new XMLHttpRequest();
        request.open("POST", location.protocol + '//' + location.host + location.pathname + 'api/dealers');
        request.send(formData);
    }

    handleChange(e) {
        this.setState({new_dealer: e.target.value});
    }

    async componentDidMount() {
        const res = await getData();
        this.setState({ dealers: res });
    }


    render() {
        let to_show;
        if (this.state.add_new){
            to_show = (<td>
                <form onSubmit={this.handleSubmit}>
                    <div className="d-flex">
                            <input className="form-control form-control-sm" type="text" placeholder="New dealer name" 
                            value={this.state.new_address} onChange={this.handleChange}/>
                            <input type="submit" className="btn btn-primary btn-sm" value="Add"/>
                            <button type="button" className="btn btn-danger btn-sm" onClick={this.handleCloseDealer}>Close</button>
                    </div>
                </form>
                </td>);
        } else {
            to_show = <button type="button" className="btn btn-info" onClick={this.handleAddDealer}>Add dealer</button>
        }

        return <table className="table table-bordered">
        <thead>
          <tr>
            <th scope="col">Name</th>
            <td scope="col">Addresses</td>
          </tr>
        </thead>
        <tbody>
            {this.state.dealers.map(el => (
                <DealerRow name={el.name} key={el.dealer_id} saleplaces={el.saleplaces} id={el.dealer_id}/>
            ))}
            <tr>
                <td>
                    {to_show}
                </td>
            </tr>
        </tbody>
      </table>
    }
}


ReactDOM.render(
    <DealersData/>,
    document.getElementById('main-box')
)