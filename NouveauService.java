package com.example.projetSEG;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;
import java.util.HashMap;

//PAGE POUR CREER UN NOUVEAU SERVICE (ADMIN)
public class NouveauService extends AppCompatActivity {

    private DatabaseReference data = FirebaseDatabase.getInstance().getReference();
    private DatabaseReference dataService = data.child("Service");

    EditText description;
    Spinner spinner;
    ArrayAdapter<CharSequence> adapter2;

    String serviceID;
    String key;

    Button creer, cancel, accept;

    ArrayList<String> idList;
    ArrayList<String> serviceList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_nouveau_service);

        spinner = findViewById(R.id.spinner);
        adapter2 = ArrayAdapter.createFromResource(this, R.array.role, R.layout.support_simple_spinner_dropdown_item);
        spinner.setAdapter(adapter2);
        description = findViewById(R.id.description);

        creer = findViewById(R.id.buttonCreerService);
        cancel = findViewById(R.id.btnCancelChange);
        accept = findViewById(R.id.btnAcceptChange);

        Intent intent = getIntent();
        serviceID = intent.getStringExtra("service");

        //DISTINCTION ENTRE creer ET modifier
        if (serviceID == null) {

            accept.setVisibility(View.GONE);
            cancel.setVisibility(View.GONE);
            creer.setVisibility(View.VISIBLE);

        } else {
            accept.setVisibility(View.VISIBLE);
            cancel.setVisibility(View.VISIBLE);
            creer.setVisibility(View.GONE);
        }

        idList = new ArrayList<>();
        serviceList = new ArrayList<>();

    }

    //LIRE DATABASE
    @Override
    protected void onStart() {
        super.onStart();
        dataService.addValueEventListener((new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {

                for (DataSnapshot postSnapshot : dataSnapshot.getChildren()) {
                    //GET INFO DATABASE

                    HashMap info = (HashMap) postSnapshot.getValue();
                    key = postSnapshot.getKey();
                    String serviceInfo = (String) info.get("id");
                    String serviceUser = (String) info.get("service");

                    if (serviceID != null) {
                        if (serviceID.equals(key)) {
                            description.setText(serviceInfo);
                            spinner.setSelection(adapter2.getPosition(serviceUser));
                        }
                    }

                    idList.add(serviceInfo);
                    serviceList.add(serviceUser);

                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {
            }
        }));


    }

    //CREER SERVICE FIREBASE
    public void Creation (View view) {

        if (alreadyCreated(description.getText().toString(), spinner.getSelectedItem().toString())) {
            Toast.makeText(getApplicationContext(), "Le service existe déjà", Toast.LENGTH_LONG).show();
        } else if (description.getText().toString().equals("")) {
            Toast.makeText(getApplicationContext(), "Veuillez donner une description", Toast.LENGTH_LONG).show();
        } else if (spinner.getSelectedItem().toString().equals("")) {
            Toast.makeText(getApplicationContext(), "Veuillez choisir un role", Toast.LENGTH_LONG).show();
        } else {

            ServiceObject newService = new ServiceObject(description.getText().toString(), spinner.getSelectedItem().toString());
            dataService.push().setValue(newService);

            Intent intent = new Intent(NouveauService.this, Administrateur.class);
            intent.putExtra("nouveauService", "Le service à bien été créé");
            startActivity(intent);
        }
    }

    public void accept(View view) {

        if (alreadyCreated(description.getText().toString(), spinner.getSelectedItem().toString())) {
            Toast.makeText(getApplicationContext(), "Le service existe déjà", Toast.LENGTH_LONG).show();
        } else if (description.getText().toString().equals("")) {
            Toast.makeText(getApplicationContext(), "Veuillez donner une description", Toast.LENGTH_LONG).show();
        } else if (spinner.getSelectedItem().toString().equals("")) {
            Toast.makeText(getApplicationContext(), "Veuillez choisir un role", Toast.LENGTH_LONG).show();
        } else {

            ServiceObject newService = new ServiceObject(description.getText().toString(), spinner.getSelectedItem().toString());
            dataService.child(serviceID).setValue(newService);

            Intent intent = new Intent(NouveauService.this, Administrateur.class);
            intent.putExtra("nouveauService", "La modification du service est accepter");
            startActivity(intent);
        }

    }

    //METHOD TO GO BACK
    public void cancel(View view) {

        Intent intent = new Intent(NouveauService.this, Administrateur.class);
        intent.putExtra("nouveauService", "La modification du service est annuler");
        startActivity(intent);

    }


    private boolean alreadyCreated (String id, String service) {
        boolean used = false;
        for (int i = 0; i < idList.size(); i++) {
            if (id.equals(idList.get(i)) && service.equals(serviceList.get(i))) {
                used = true;
            }
        }
        return used;
    }
}
