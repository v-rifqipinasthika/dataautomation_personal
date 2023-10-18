using System;
using System.Collections.Generic;
using UiPath.CodedWorkflows;
using UiPath.Testing;
using UiPath.Testing.Activities.TestData;
using UiPath.Testing.Activities.TestDataQueues.Enums;
using UiPath.Testing.Enums;

namespace Traveloka_DataAutomation_Dispatcher_SFTP
{
    public partial class CodedWorkflow : CodedWorkflowBase
    {
        public CodedWorkflow()
        {
            _ = new System.Type[]{typeof(UiPath.Testing.API.ITestingService)};
        }

        protected UiPath.Testing.API.ITestingService testing { get => serviceContainer.Resolve<UiPath.Testing.API.ITestingService>() ; }
    }
}