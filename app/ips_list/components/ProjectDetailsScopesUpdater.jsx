import _ from 'lodash'
import React from 'react'
import { Dimmer, Loader, Segment } from 'semantic-ui-react'

import ProjectDetails from './ProjectDetails.jsx'
import ScopesSocketioEventsEmitter from '../../redux/scopes/ScopesSocketioEventsEmitter.js'


class ProjectDetailsScopesUpdater extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			loading: false
		}

		this.scopesEmitter = new ScopesSocketioEventsEmitter();
		this.setLoading = this.setLoading.bind(this);

		var { ips, hosts } = this.props;

		if (this.props.update_needed === true) {
			this.scopesEmitter.requestRenewScopes(
				this.props.project_uuid, ips.ip_page, ips.ip_page_size, hosts.host_page, hosts.host_page);
		}
	}

	setLoading(value) {
		this.setState({
			loading: value
		});
	}

	componentWillReceiveProps(nextProps) {
		var { ips, hosts } = nextProps.scopes;

		if ((nextProps.scopes.update_needed === true) || (!_.isEqual(nextProps.filters, this.props.filters))) {
			this.scopesEmitter.requestRenewScopes(
				this.props.project.project_uuid, nextProps.filters,
				ips.page, ips.page_size,
				hosts.page, hosts.page_size);
		}

		if (this.state.loading) {
			this.setLoading(false);
		}

		// if ((ips.page !== this.props.scopes.ips.page) || (ips.page_size !== this.props.scopes.ips.page_size)
		// 	|| (JSON.stringify(ips.data) !== JSON.stringify(this.props.scopes.ips.data))) {
		// 	this.setLoading(false);
		// }		
	}

	render() {
		return (
			<Segment vertical>
				<Dimmer active={this.state.loading} inverted>
					<Loader />
				</Dimmer>			
				<ProjectDetails setLoading={this.setLoading} {...this.props} />
			</Segment>
		)
	}
}

export default ProjectDetailsScopesUpdater;