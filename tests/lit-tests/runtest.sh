set -ex


if ! id -u lld; then
	useradd lld
fi

su lld -c 'bash /usr/libexec/tests/lld/run-lit-tests --threads 1'
