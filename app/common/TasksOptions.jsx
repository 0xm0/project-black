import _ from 'lodash'
import React from 'react'
import { Button, Modal, MenuItem } from 'react-bootstrap'


class TasksOptions extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			showModal: false
		}

		this.open = this.open.bind(this);
		this.close = this.close.bind(this);
		this.startTask = this.startTask.bind(this);
	}

	close() {
		this.setState({ showModal: false });
	}	

	open() {
		this.setState({ showModal: true });
	}

	startTask(options) {
		this.props.task.handler(options)
		this.close()
	}

	render() {
		const startButtons = _.map(this.props.task.preformed_options, (x) => {
			return <Button key={x.name} onClick={() => this.startTask(x.options)}>{x.name}</Button>
		});

		return ( 
			<MenuItem key={this.props.number}
					  eventKey={this.props.number}
					  onClick={this.open} >
				{this.props.task.name}
				<Modal show={this.state.showModal} onHide={this.close} >
					<Modal.Header closeButton>
						<Modal.Title>Prepared settings</Modal.Title>
					</Modal.Header>
					<Modal.Body>
						<h4>Choose one of the prepared options or create your own</h4>
						{startButtons}
						<hr />
					</Modal.Body>
					<Modal.Footer>
						<Button onClick={this.close}>Close</Button>
					</Modal.Footer>
				</Modal>
			</MenuItem>
		)
	}
}

export default TasksOptions;