FROM public.ecr.aws/lambda/python:3.9

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Copy function code
COPY letsdata_lambda_function.py ${LAMBDA_TASK_ROOT}

RUN mkdir -p ${LAMBDA_TASK_ROOT}/letsdata_interfaces
COPY letsdata_interfaces/ ${LAMBDA_TASK_ROOT}/letsdata_interfaces/

RUN mkdir -p ${LAMBDA_TASK_ROOT}/letsdata_service
COPY letsdata_service/ ${LAMBDA_TASK_ROOT}/letsdata_service/

RUN mkdir -p ${LAMBDA_TASK_ROOT}/letsdata_utils
COPY letsdata_utils/ ${LAMBDA_TASK_ROOT}/letsdata_utils/

# Install the specified packages
RUN pip install -r requirements.txt

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "letsdata_lambda_function.lambda_handler" ]