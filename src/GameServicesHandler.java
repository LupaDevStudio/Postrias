package org.org.kivygameservices;

import android.content.Context;
import android.content.IntentSender;
import android.os.Bundle;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.games.GamesSignInClient;
import com.google.android.gms.games.PlayGamesSdk;
import com.google.android.gms.games.Players;

public class GameServicesHandler
        implements GoogleApiClient.ConnectionCallbacks, GoogleApiClient.OnConnectionFailedListener {

    private static final int REQUEST_LEADERBOARD = 1;
    private GoogleApiClient mGoogleApiClient;
    private Context mContext;

    public GameServicesHandler(Context context) {
        mContext = context;
        PlayGamesSdk.initialize(context);

        // Initialize the Play Games SDK
        mGoogleApiClient = new GoogleApiClient.Builder(context)
                .addConnectionCallbacks(this)
                .addOnConnectionFailedListener(this)
                .addApi(Games.API)
                .build();
    }

    public void connect() {
        // Connect to Play Games services
        mGoogleApiClient.connect();
    }

    public void disconnect() {
        // Disconnect from Play Games services
        mGoogleApiClient.disconnect();
    }

    // public void showLeaderboard() {
    // GamesSignInClient gamesSignInClient =
    // PlayGamesSdk.getGamesSignInClient(mContext);

    // gamesSignInClient.isAuthenticated().addOnCompleteListener(isAuthenticatedTask
    // -> {
    // boolean isAuthenticated = (isAuthenticatedTask.isSuccessful() &&
    // isAuthenticatedTask.getResult().isAuthenticated());

    // if (isAuthenticated) {
    // // Continue with Play Games Services
    // // You can add the code to show the leaderboard here
    // showLeaderboardInternal();
    // } else {
    // // Disable your integration with Play Games Services or show a
    // // login button to ask players to sign-in. Clicking it should
    // // call GamesSignInClient.signIn().
    // // Handle the sign-in logic as needed in your application
    // }
    // });
    // }

    // private void showLeaderboardInternal() {
    // // Retrieve the Player ID
    // Players.getPlayersClient(mContext).getCurrentPlayer().addOnCompleteListener(task
    // -> {
    // String playerId = task.getResult().getPlayerId();
    // // You can use the playerId for further processing or displaying information
    // // about the current player.
    // // Example: Log.d("GameServicesHandler", "Player ID: " + playerId);

    // // Add your code to show the leaderboard using the retrieved Player ID
    // // For example:
    // //
    // Games.getLeaderboardsClient(mGoogleApiClient).getLeaderboardIntent("YOUR_LEADERBOARD_ID")
    // // .addOnSuccessListener(intent -> {
    // // // Start the intent to show the leaderboard
    // // })
    // // .addOnFailureListener(e -> {
    // // // Handle error
    // // });
    // });
    // }

    // Override methods for GoogleApiClient.ConnectionCallbacks
    @Override
    public void onConnected(Bundle bundle) {
        // Connected to Play Games services
    }

    @Override
    public void onConnectionSuspended(int i) {
        // Connection suspended
    }

    // Override method for GoogleApiClient.OnConnectionFailedListener
    @Override
    public void onConnectionFailed(ConnectionResult connectionResult) {
        // Connection failed
        if (connectionResult.hasResolution()) {
            try {
                connectionResult.startResolutionForResult(null, REQUEST_LEADERBOARD);
            } catch (IntentSender.SendIntentException e) {
                // Handle error
            }
        }
    }
}
