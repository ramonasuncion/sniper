defmodule Sniper.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    # Load .env file from project root
    load_dotenv()

    children = [
      {Sniper.PythonBridge, []},
      {Plug.Cowboy, scheme: :http, plug: Sniper.Webhook, options: [port: 4000]}
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: Sniper.Supervisor]
    Supervisor.start_link(children, opts)
  end

  # Load environment variables from .env file if it exists
  defp load_dotenv do
    env_path = Path.join(File.cwd!(), ".env")

    if File.exists?(env_path) do
      Dotenvy.source!([env_path], side_effect: :system)
    end
  end
end
